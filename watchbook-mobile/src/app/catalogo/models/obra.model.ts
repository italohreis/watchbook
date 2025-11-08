export class Obra {
    public id: number;
    public titulo: string;
    public ano_lancamento: number;
    public diretor: string;
    public genero: string;
    public poster: string | undefined;
    public tipo: string;
    public tipo_display: string;

    constructor() {
        this.id = 0;
        this.titulo = '';
        this.ano_lancamento = 0;
        this.diretor = '';
        this.genero = '';
        this.tipo = 'filme';
        this.tipo_display = 'Filme';
    }
}
