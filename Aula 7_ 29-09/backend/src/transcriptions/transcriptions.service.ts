import { BadGatewayException, Injectable, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Transcription } from './entities/transcription.entity';

@Injectable()
export class TranscriptionsService {
  private readonly logger = new Logger(TranscriptionsService.name);

  constructor(
    private readonly configService: ConfigService,
    @InjectRepository(Transcription)
    private readonly transcriptionRepository: Repository<Transcription>,
  ) {}

  async create(
    userId: string,
    file: Buffer,
    originalFilename: string,
  ): Promise<Transcription> {
    const groqApiKey = this.configService.getOrThrow<string>('GROQ_API_KEY');
    const groqModel = this.configService.getOrThrow<string>('GROQ_MODEL');

    const blob = new Blob([file as any], { type: 'audio/*' });
    const formData = new FormData();
    formData.append('file', blob, originalFilename);
    formData.append('model', groqModel);
    formData.append('language', 'pt');

    let text: string;
    try {
      const response = await fetch(
        'https://api.groq.com/openai/v1/audio/transcriptions',
        {
          method: 'POST',
          headers: { Authorization: `Bearer ${groqApiKey}` },
          body: formData,
        },
      );
      if (!response.ok) {
        const detail = await response.text();
        this.logger.error(`Groq respondeu ${response.status}: ${detail}`);
        throw new BadGatewayException('Falha na transcri\u00e7\u00e3o (Groq)');
      }
      const result = (await response.json()) as { text?: string };
      if (typeof result.text !== 'string') {
        throw new Error('Resposta da Groq sem o campo text');
      }
      text = result.text;
    } catch (error) {
      if (error instanceof BadGatewayException) {
        throw error;
      }
      this.logger.error(
        'Erro ao chamar a Groq',
        error instanceof Error ? error.stack : String(error),
      );
      throw new BadGatewayException('Falha na transcri\u00e7\u00e3o (Groq)');
    }

    const transcription = this.transcriptionRepository.create({
      userId,
      text,
      originalFilename,
    });
    return this.transcriptionRepository.save(transcription);
  }

  async findAllByUser(userId: string): Promise<Transcription[]> {
    return this.transcriptionRepository.find({
      where: { userId },
      order: { createdAt: 'DESC' },
    });
  }
}