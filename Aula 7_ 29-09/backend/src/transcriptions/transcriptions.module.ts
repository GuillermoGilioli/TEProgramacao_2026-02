import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Transcription } from './entities/transcription.entity';
import { TranscriptionsService } from './transcriptions.service';
import { TranscriptionsController } from './transcriptions.controller';
import { ConfigModule, ConfigService } from '@nestjs/config';

@Module({
  imports: [
    TypeOrmModule.forFeature([Transcription]),
  ],
  providers: [TranscriptionsService],
  controllers: [TranscriptionsController],
  exports: [TranscriptionsService],
})
export class TranscriptionsModule {}