import { Body, Controller, Post, Get, UseInterceptors, UploadedFile, BadRequestException, HttpCode, HttpStatus } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { CurrentUser } from '../common/decorators/current-user.decorator';
import { TranscriptionsService } from './transcriptions.service';
import { Transcription } from './entities/transcription.entity';

const AUDIO_MIME_TYPES = [
  'audio/mpeg',
  'audio/mp3',
  'audio/wav',
  'audio/x-wav',
  'audio/m4a',
  'audio/ogg',
  'audio/webm',
  'audio/flac',
  'video/mp4',
  'video/mpeg',
];

@Controller('transcriptions')
export class TranscriptionsController {
  constructor(private readonly transcriptionsService: TranscriptionsService) {}

  @Get()
  findAllByUser(@CurrentUser('id') userId: string): Promise<Transcription[]> {
    return this.transcriptionsService.findAllByUser(userId);
  }

  @Post()
  @UseInterceptors(FileInterceptor('file', {
    limits: { fileSize: 25 * 1024 * 1024 },
    fileFilter: (req, file, cb) => {
      const ext = (file.originalname.split('.').pop() || '').toLowerCase();
      const mimeType = file.mimetype;
      const acceptedExtensions = ['mp3', 'm4a', 'wav', 'ogg', 'webm', 'flac', 'mp4', 'mpeg'];
      const acceptedMimeTypes = AUDIO_MIME_TYPES;

      const isValidExtension = acceptedExtensions.includes(ext);
      const isValidMimeType = acceptedMimeTypes.includes(mimeType);

      if (!isValidExtension && !isValidMimeType) {
        cb(new BadRequestException('Formato de áudio inválido') as any, false);
        return;
      }

      cb(null, true);
    },
  }))
  async create(
    @CurrentUser('id') userId: string,
    @Body() body: {},
    @UploadedFile() file: any,
  ) {
    if (!file) {
      throw new BadRequestException('Arquivo é obrigatório');
    }

    return this.transcriptionsService.create(userId, file.buffer, file.originalname || 'audio');
  }
}