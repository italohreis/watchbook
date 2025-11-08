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
  IonCardContent,
  IonList,
  IonItem,
  IonLabel,
  IonIcon,
  IonButton,
  IonAvatar
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Usuario } from '../login/models/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppHeaderComponent } from '../components/app-header/app-header.component';
import { addIcons } from 'ionicons';
import {
  personOutline,
  mailOutline,
  filmOutline,
  peopleOutline,
  starOutline,
  logOutOutline
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
    IonText,
    IonContent,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonIcon,
    CommonModule,
    FormsModule
  ],
  providers: [Storage]
})
export class PerfilPage implements OnInit {

  public usuario: Usuario = new Usuario();
  public perfil = {
    total_obras: 0,
    total_filmes: 0,
    total_series: 0,
    genero_favorito: '',
    nota_media: 0,
    total_amigos: 0
  };

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController
  ) {
    // Registra os ícones
    addIcons({
      'person-outline': personOutline,
      'mail-outline': mailOutline,
      'film-outline': filmOutline,
      'people-outline': peopleOutline,
      'star-outline': starOutline,
      'log-out-outline': logOutOutline
    });
  }

  async ngOnInit() {
    // Verifica se existe registro de configuração para o último usuário autenticado
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.carregarPerfil();
    } else {
      this.controle_navegacao.navigateRoot('/login');
    }
  }

  async carregarPerfil() {
    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({
      message: 'Carregando perfil...',
      duration: 60000
    });
    await loading.present();

    // Define informações do cabeçalho da requisição
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: 'http://127.0.0.1:8000/api/usuarios/meu_perfil/'
    };

    CapacitorHttp.get(options)
      .then(async (resposta: HttpResponse) => {
        // Verifica se a requisição foi processada com sucesso
        if (resposta.status == 200) {
          this.perfil.total_obras = resposta.data.total_obras;
          this.perfil.total_filmes = resposta.data.total_filmes;
          this.perfil.total_series = resposta.data.total_series;
          this.perfil.genero_favorito = resposta.data.genero_favorito;
          this.perfil.nota_media = resposta.data.nota_media;
          this.perfil.total_amigos = resposta.data.total_amigos;

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

  async sair() {
    // Faz logout na API
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: 'http://127.0.0.1:8000/api/logout/'
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
