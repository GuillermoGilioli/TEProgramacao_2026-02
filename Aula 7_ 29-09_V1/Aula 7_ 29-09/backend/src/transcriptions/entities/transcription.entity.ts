import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

@Entity('transcriptions')
export class Transcription {
  @PrimaryGeneratedColumn('uuid')
  id!: string;

  @Column({ type: 'uuid' })
  userId!: string;

  @Column({ type: 'text' })
  text!: string;

  @Column()
  originalFilename!: string;

  @CreateDateColumn({ type: 'timestamptz' })
  createdAt!: Date;
}