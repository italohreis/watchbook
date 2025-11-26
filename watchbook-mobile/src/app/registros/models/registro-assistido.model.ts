export class RegistroAssistido {
    public id: number;
    public obra: {
        id: number;
        titulo: string;
        ano_lancamento: number;
        diretor: string;
        genero: string;
        poster: string;
        tipo: string;
        tipo_display: string;
    };
    public nota: number;
    public critica: string;
    public data_assistido: string;

    constructor() {
        this.id = 0;
        this.obra = {
            id: 0,
            titulo: '',
            ano_lancamento: 0,
            diretor: '',
            genero: '',
            poster: '',
            tipo: 'filme',
            tipo_display: 'Filme'
        };
        this.nota = 0;
        this.critica = '';
        this.data_assistido = '';
    }
}
