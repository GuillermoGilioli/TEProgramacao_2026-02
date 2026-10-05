import { IsEmail, IsString, Length, Matches, MinLength } from 'class-validator';

export class RegisterDto {
  @IsString()
  @Length(2, 100)
  name!: string;

  @IsEmail()
  email!: string;

  @IsString()
  @MinLength(8, { message: 'A senha deve ter pelo menos 8 caracteres' })
  @Matches(/[A-Z]/, { message: 'A senha deve ter uma letra mai\u00fascula' })
  @Matches(/[a-z]/, { message: 'A senha deve ter uma letra min\u00fascula' })
  @Matches(/\d/, { message: 'A senha deve ter um n\u00famero' })
  @Matches(/[^A-Za-z0-9]/, {
    message: 'A senha deve ter um caractere especial',
  })
  password!: string;
}