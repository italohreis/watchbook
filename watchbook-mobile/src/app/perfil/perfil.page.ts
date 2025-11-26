import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, ActivatedRoute } from '@angular/router';
import {
  IonContent,
  LoadingController,
  NavController,
  ToastController,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonList,
  IonItem,
  IonLabel,
  IonIcon,
  IonButton,
  IonAvatar,
  IonThumbnail
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Usuario } from '../login/models/usuario.model';
import { Registro } from '../inicio/models/registro.model';
import { PerfilData } from './models/perfil-data.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppHeaderComponent } from '../components/app-header/app-header.component';
import { environment } from '../../environments/environment';
import { addIcons } from 'ionicons';
import {
  personOutline,
  atOutline,
  filmOutline,
  peopleOutline,
  star,
  heart,
  videocamOutline,
  tvOutline,
  barChartOutline,
  logOutOutline,
  listOutline,
  timeOutline
} from 'ionicons/icons';

@Component({
  standalone: true,
  selector: 'app-perfil',
  templateUrl: './perfil.page.html',
  styleUrls: ['./perfil.page.scss'],
  imports: [
    AppHeaderComponent,
    IonAvatar,
    IonButton,
    IonLabel,
    IonItem,
    IonList,
    IonCardContent,
    IonCardTitle,
    IonCardHeader,
    IonCard,
    IonContent,
    IonIcon,
    IonThumbnail,
    RouterLink,
    CommonModule,
    FormsModule
  ],
  providers: [Storage]
})
export class PerfilPage implements OnInit {

  public usuario: Usuario = new Usuario();
  public usuario_id: number | null = null; // ID do usuário sendo visualizado (null = próprio perfil)
  public perfil: PerfilData = {
    total_obras: 0,
    total_filmes: 0,
    total_series: 0,
    genero_favorito: '',
    nota_media: 0,
    total_amigos: 0
  };
  public registros_recentes: Registro[] = [];

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    private route: ActivatedRoute
  ) {
    // Registra os ícones
    addIcons({
      'person-outline': personOutline,
      'at-outline': atOutline,
      'film-outline': filmOutline,
      'people-outline': peopleOutline,
      'star': star,
      'heart': heart,
      'videocam-outline': videocamOutline,
      'tv-outline': tvOutline,
      'bar-chart-outline': barChartOutline,
      'log-out-outline': logOutOutline,
      'list-outline': listOutline,
      'time-outline': timeOutline
    });
  }

  async ngOnInit() {
    // Verifica se existe registro de configuração para o último usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);

      // Verifica se há um ID na rota (visualizando outro usuário)
      this.route.params.subscribe(params => {
        if (params['id']) {
          this.usuario_id = +params['id'];
        }
        this.carregarPerfil();
      });
    } else {
      this.controle_navegacao.navigateRoot('/login');
    }
  }

  // Retorna true se está visualizando o próprio perfil
  get isPerfilProprio(): boolean {
    return this.usuario_id === null;
  }

  // Retorna o título da página
  get pageTitle(): string {
    if (this.isPerfilProprio) {
      return 'Perfil';
    }
    return this.perfil.username ? `@${this.perfil.username}` : 'Perfil';
  }

  async carregarPerfil() {
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({
      message: 'Carregando perfil...',
      duration: 60000
    });
    await loading.present();

    // Define a URL com base em qual perfil está sendo visualizado
    const url = this.isPerfilProprio
      ? `${environment.apiUrl}/usuarios/meu_perfil/`
      : `${environment.apiUrl}/usuarios/${this.usuario_id}/perfil/`;

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
          this.perfil = resposta.data;

          // Carrega registros recentes
          this.carregarRegistrosRecentes();

          // Finaliza interface com efeito de carregamento
          loading.dismiss();
        } else {
          // Finaliza e apresenta mensagem de erro
          loading.dismiss();
          this.apresenta_mensagem(`Falha ao carregar perfil: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao carregar perfil: código ${erro?.status}`);
      });
  }

  async carregarRegistrosRecentes() {
    // Define a URL com base em qual perfil está sendo visualizado
    const url = this.isPerfilProprio
      ? `${environment.apiUrl}/registros/?limit=5`
      : `${environment.apiUrl}/usuarios/${this.usuario_id}/registros/`;

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: url
    };

    CapacitorHttp.get(options)
      .then((resposta: HttpResponse) => {
        if (resposta.status == 200) {
          this.registros_recentes = resposta.data.slice(0, 5);
        }
      })
      .catch((erro: any) => {
        console.log('Erro ao carregar registros recentes:', erro);
      });
  }

  gerarEstrelas(nota: number): boolean[] {
    return Array(5).fill(false).map((_, i) => i < nota);
  }

  obterUrlPoster(poster: string | undefined): string {
    if (poster && poster.startsWith('http')) {
      return poster;
    } else if (poster) {
      return `${environment.apiUrl.replace('/api', '')}${poster}`;
    }
    return 'assets/placeholder-poster.png';
  }

  verRegistros() {
    if (!this.isPerfilProprio && this.perfil.id && this.perfil.username) {
      this.controle_navegacao.navigateForward(`/registros-usuario/${this.perfil.id}`, {
        state: { username: this.perfil.username }
      });
    }
  }

  async sair() {
    // Faz logout na API
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/logout/`
    };

    CapacitorHttp.post(options)
      .then(async (resposta: HttpResponse) => {
        // Remove credenciais localmente
        await this.storage.remove('usuario');
        this.controle_navegacao.navigateRoot('/login');
      })
      .catch(async (erro: any) => {
        // Mesmo com erro, remove credenciais localmente
        await this.storage.remove('usuario');
        this.controle_navegacao.navigateRoot('/login');
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
}
