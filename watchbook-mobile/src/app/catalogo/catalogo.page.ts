import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent,
  IonHeader,
  IonTitle,
  IonToolbar,
  LoadingController,
  NavController,
  ToastController,
  IonText,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonList,
  IonItem,
  IonThumbnail,
  IonLabel,
  IonIcon,
  IonButton,
  IonSearchbar,
  IonBadge,
  IonCol,
  IonRow,
  IonGrid
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Obra } from './models/obra.model';
import { Usuario } from '../login/models/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppHeaderComponent } from '../components/app-header/app-header.component';
import { TipoFilterComponent } from '../components/tipo-filter/tipo-filter.component';
import { addIcons } from 'ionicons';
import {
  searchOutline,
  filmOutline,
  tvOutline,
  gridOutline,
  calendarOutline,
  personOutline
} from 'ionicons/icons';

@Component({
  standalone: true,
  selector: 'app-catalogo',
  templateUrl: './catalogo.page.html',
  styleUrls: ['./catalogo.page.scss'],
  imports: [
    AppHeaderComponent,
    TipoFilterComponent,
    IonGrid,
    IonRow,
    IonCol,
    IonBadge,
    IonLabel,
    IonItem,
    IonList,
    IonCardContent,
    IonCardSubtitle,
    IonCardTitle,
    IonCardHeader,
    IonCard,
    IonText,
    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonThumbnail,
    IonIcon,
    IonButton,
    IonSearchbar,
    CommonModule,
    FormsModule
  ],
  providers: [Storage]
})
export class CatalogoPage implements OnInit {

  public usuario: Usuario = new Usuario();
  public lista_obras: Obra[] = [];
  public tipo_filtro: string = 'todos';
  public termo_busca: string = '';

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController
  ) {
    // Registra os ícones
    addIcons({
      'search-outline': searchOutline,
      'film-outline': filmOutline,
      'tv-outline': tvOutline,
      'grid-outline': gridOutline,
      'calendar-outline': calendarOutline,
      'person-outline': personOutline
    });
  }

  async ngOnInit() {
    // Verifica se existe registro de configuração para o último usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.consultarObrasSistemaWeb();
    } else {
      this.controle_navegacao.navigateRoot('/login');
    }
  }

  async consultarObrasSistemaWeb() {
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({
      message: 'Pesquisando obras...',
      duration: 60000
    });
    await loading.present();

    // Monta a URL com filtros
    let url = 'http://127.0.0.1:8000/api/catalogo/';
    const params: string[] = [];

    if (this.tipo_filtro !== 'todos') {
      params.push(`tipo=${this.tipo_filtro}`);
    }

    if (this.termo_busca.trim()) {
      params.push(`q=${encodeURIComponent(this.termo_busca)}`);
    }

    if (params.length > 0) {
      url += '?' + params.join('&');
    }

    // Define informações do cabeçalho da requisição
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: url
    };

    CapacitorHttp.get(options)
      .then(async (resposta: HttpResponse) => {
        // Verifica se a requisição foi processada com sucesso
        if (resposta.status == 200) {
          this.lista_obras = resposta.data;

          // Finaliza interface com efeito de carregamento
          loading.dismiss();
        } else {
          // Finaliza e apresenta mensagem de erro
          loading.dismiss();
          this.apresenta_mensagem(`Falha ao consultar obras: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao consultar obras: código ${erro?.status}`);
      });
  }

  async filtrarPorTipo(event: any) {
    this.tipo_filtro = event;
    this.consultarObrasSistemaWeb();
  }

  async buscarObra(event: any) {
    this.termo_busca = event.target.value;
    if (this.termo_busca.length >= 3 || this.termo_busca.length === 0) {
      this.consultarObrasSistemaWeb();
    }
  }

  async limparBusca() {
    this.termo_busca = '';
    this.consultarObrasSistemaWeb();
  }

  async apresenta_mensagem(texto: string) {
    const mensagem = await this.controle_toast.create({
      message: texto,
      cssClass: 'ion-text-center',
      duration: 2000
    });
    mensagem.present();
  }

  obterUrlPoster(poster: string | undefined): string {
    if (poster && poster.startsWith('http')) {
      return poster;
    } else if (poster) {
      return `http://127.0.0.1:8000${poster}`;
    }
    return 'assets/placeholder-poster.png';
  }
}
