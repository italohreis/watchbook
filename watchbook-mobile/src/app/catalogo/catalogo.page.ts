import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent,
  LoadingController,
  NavController,
  ToastController,
  ModalController,
  IonText,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonThumbnail,
  IonIcon,
  IonButton,
  IonSearchbar,
  IonBadge,
  IonCol,
  IonRow,
  IonGrid
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { environment } from '../../environments/environment';
import { Obra } from './models/obra.model';
import { Usuario } from '../login/models/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppHeaderComponent } from '../components/app-header/app-header.component';
import { TipoFilterComponent } from '../components/tipo-filter/tipo-filter.component';
import { ModalAdicionarRegistroComponent } from './modal-adicionar-registro/modal-adicionar-registro.component';
import { addIcons } from 'ionicons';
import {
  searchOutline,
  filmOutline,
  tvOutline,
  gridOutline,
  calendarOutline,
  personOutline,
  addCircle
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
    IonCardContent,
    IonCardSubtitle,
    IonCardTitle,
    IonCardHeader,
    IonCard,
    IonText,
    IonContent,
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
    public controle_carregamento: LoadingController,
    public controle_modal: ModalController
  ) {
    // Registra os ícones
    addIcons({
      'search-outline': searchOutline,
      'film-outline': filmOutline,
      'tv-outline': tvOutline,
      'grid-outline': gridOutline,
      'calendar-outline': calendarOutline,
      'person-outline': personOutline,
      'add-circle': addCircle
    });
  }

  async ngOnInit() {
    // Verifica se existe registro de configuração para o último usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.consultarObrasSistema();
    } else {
      this.controle_navegacao.navigateRoot('/login');
    }
  }

  async consultarObrasSistema() {
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({
      message: 'Pesquisando obras...',
      duration: 60000
    });
    await loading.present();

    // Monta a URL com filtros
    let url = `${environment.apiUrl}/catalogo/`;
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
    this.consultarObrasSistema();
  }

  async buscarObra() {
    this.consultarObrasSistema();
  }

  async limparBusca() {
    this.termo_busca = '';
    this.consultarObrasSistema();
  }

  async abrirModalAdicionar(obra: Obra) {
    const modal = await this.controle_modal.create({
      component: ModalAdicionarRegistroComponent,
      componentProps: {
        obra: obra
      }
    });

    modal.present();

    const { data, role } = await modal.onWillDismiss();

    if (role === 'salvar' && data) {
      this.adicionarRegistro(data);
    }
  }

  async adicionarRegistro(dados: any) {
    const loading = await this.controle_carregamento.create({
      message: 'Adicionando aos assistidos...',
      duration: 60000
    });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/registros/`,
      data: dados
    };

    CapacitorHttp.post(options)
      .then(async (resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 201 || resposta.status == 200) {
          this.apresenta_mensagem('Obra adicionada aos assistidos!');
        } else {
          this.apresenta_mensagem(`Falha ao adicionar: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao adicionar: ${erro?.message || 'Erro desconhecido'}`);
      });
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
      return `${environment.apiUrl.replace('/api', '')}${poster}`;
    }
    return 'assets/placeholder-poster.png';
  }
}
