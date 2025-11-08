export class Registro {
    public id: number;
    public usuario: number;
    public usuario_nome: string;
    public obra: {
        id: number;
        titulo: string;
        poster: string | undefined;
        tipo: string;
        tipo_display: string;
        genero: string;
        ano_lancamento: number;
        diretor: string;
    };
    public nota: number;
    public critica: string;
    public data_assistido: string;

    constructor() {
        this.id = 0;
        this.usuario = 0;
        this.usuario_nome = '';
        this.obra = {
            id: 0,
            titulo: '',
            poster: undefined,
            tipo: 'filme',
            tipo_display: 'Filme',
            genero: '',
            ano_lancamento: 0,
            diretor: ''
        };
        this.nota = 0;
        this.critica = '';
        this.data_assistido = '';
    }
}
