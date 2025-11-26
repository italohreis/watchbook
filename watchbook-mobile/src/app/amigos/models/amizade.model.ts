export class Amizade {
    public id: number;
    public de_usuario: {
        id: number;
        username: string;
        first_name: string;
    };
    public para_usuario: {
        id: number;
        username: string;
        first_name: string;
    };
    public status: string;
    public status_display: string;
    public data_criacao: string;

    constructor() {
        this.id = 0;
        this.de_usuario = {
            id: 0,
            username: '',
            first_name: ''
        };
        this.para_usuario = {
            id: 0,
            username: '',
            first_name: ''
        };
        this.status = '';
        this.status_display = '';
        this.data_criacao = '';
    }
}
