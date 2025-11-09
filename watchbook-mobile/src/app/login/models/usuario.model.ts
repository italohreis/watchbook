export class Usuario
{
  public id: number;
  public first_name: string;
  public username: string;
  public token: string;

  constructor() { 
    this.id = 0;
    this.first_name = '';
    this.username = '';
    this.token = '';
  }
}