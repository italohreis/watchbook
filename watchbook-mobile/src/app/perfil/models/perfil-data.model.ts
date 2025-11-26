export class PerfilData {
    public id?: number;
    public username?: string;
    public total_obras: number;
    public total_filmes: number;
    public total_series: number;
    public genero_favorito: string | null;
    public nota_media: number | null;
    public total_amigos: number;

    constructor() {
        this.id = undefined;
        this.username = undefined;
        this.total_obras = 0;
        this.total_filmes = 0;
        this.total_series = 0;
        this.genero_favorito = null;
        this.nota_media = null;
        this.total_amigos = 0;
    }
}
