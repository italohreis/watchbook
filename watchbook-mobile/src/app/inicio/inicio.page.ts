import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import {
  IonContent,
  IonHeader,
  IonTitle,
  IonToolbar,
  IonButton,
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
  IonBadge,
  IonRefresher,
  IonRefresherContent
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Registro } from './models/registro.model';
import { Usuario } from '../login/models/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppHeaderComponent } from '../components/app-header/app-header.component';
import { environment } from '../../environments/environment';
import { addIcons } from 'ionicons';
import {
  homeOutline,
  starOutline,
  star,
  calendarOutline,
  filmOutline,
  peopleOutline
} from 'ionicons/icons';

@Component({
  standalone: true,
  selector: 'app-inicio',
  templateUrl: './inicio.page.html',
  styleUrls: ['./inicio.page.scss'],
  imports: [
    AppHeaderComponent,
    RouterLink,
    IonButton,
    IonRefresherContent,
    IonRefresher,
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
    CommonModule,
    FormsModule
  ],
  providers: [Storage]
})
export class InicioPage implements OnInit {

  public usuario: Usuario = new Usuario();
  public atividades_amigos: Registro[] = [];
  public meus_registros: Registro[] = [];
  public estatisticas = {
    total_obras: 0,
    total_amigos: 0
  };

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController
  ) {
    addIcons({
      'home-outline': homeOutline,
      'star-outline': starOutline,
      'star': star,
      'calendar-outline': calendarOutline,
      'film-outline': filmOutline,
      'people-outline': peopleOutline
    });
  }

  async ngOnInit() {
    // Verifica se existe registro de configuração para o último usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.carregarDados();
    } else {
      this.controle_navegacao.navigateRoot('/login');
    }
  }

  async carregarDados() {
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({
      message: 'Carregando...',
      duration: 60000
    });
    await loading.present();

    // Define informações do cabeçalho da requisição
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/inicio/`
    };

    CapacitorHttp.get(options)
      .then(async (resposta: HttpResponse) => {
        // Verifica se a requisição foi processada com sucesso
        if (resposta.status == 200) {
          this.estatisticas.total_obras = resposta.data.total_obras;
          this.estatisticas.total_amigos = resposta.data.total_amigos;
          this.atividades_amigos = resposta.data.atividades_amigos;
          this.meus_registros = resposta.data.meus_registros_recentes;

          // Finaliza interface com efeito de carregamento
          loading.dismiss();
        } else {
          // Finaliza e apresenta mensagem de erro
          loading.dismiss();
          this.apresenta_mensagem(`Falha ao carregar dados: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao carregar dados: código ${erro?.status}`);
      });
  }

  async atualizarDados(event: any) {
    await this.carregarDados();
    event.target.complete();
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

  gerarEstrelas(nota: number): boolean[] {
    return Array(5).fill(false).map((_, i) => i < nota);
  }
}
