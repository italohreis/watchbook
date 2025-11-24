import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import {
  IonContent,
  LoadingController,
  NavController,
  ToastController,
  IonText,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonIcon,
  IonBadge,
  IonGrid,
  IonRow,
  IonCol,
  IonRefresher,
  IonRefresherContent
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Usuario } from '../login/models/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppHeaderComponent } from '../components/app-header/app-header.component';
import { TipoFilterComponent } from '../components/tipo-filter/tipo-filter.component';
import { environment } from '../../environments/environment';
import { addIcons } from 'ionicons';
import {
  calendarOutline,
  personOutline,
  filmOutline,
  starOutline,
  star
} from 'ionicons/icons';

interface Registro {
  id: number;
  usuario: number;
  usuario_nome: string;
  obra: {
    id: number;
    titulo: string;
    poster: string;
    tipo: string;
    tipo_display: string;
    genero: string;
    ano_lancamento: number;
    diretor: string;
  };
  nota: number;
  critica: string;
  data_assistido: string;
}

@Component({
  selector: 'app-registros-usuario',
  templateUrl: './registros-usuario.page.html',
  styleUrls: ['./registros-usuario.page.scss'],
  standalone: true,
  imports: [
    AppHeaderComponent,
    TipoFilterComponent,
    IonContent,
    CommonModule,
    FormsModule,
    IonText,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonCardContent,
    IonIcon,
    IonBadge,
    IonGrid,
    IonRow,
    IonCol,
    IonRefresher,
    IonRefresherContent
  ],
  providers: [Storage]
})
export class RegistrosUsuarioPage implements OnInit {
  usuario: Usuario = new Usuario();
  usuario_id: number = 0;
  username: string = '';
  registros: Registro[] = [];
  registros_filtrados: Registro[] = [];
  tipo_filtro: string = 'todos';

  constructor(
    private storage: Storage,
    private controle_toast: ToastController,
    private controle_navegacao: NavController,
    private controle_carregamento: LoadingController,
    private route: ActivatedRoute,
    private router: Router
  ) {
    addIcons({
      calendarOutline,
      personOutline,
      filmOutline,
      starOutline,
      star
    });
  }

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);

      // Pega o ID da rota
      this.route.params.subscribe(params => {
        this.usuario_id = +params['id'];
      });

      // Pega o username do state
      const navigation = this.router.getCurrentNavigation();
      if (navigation?.extras?.state) {
        this.username = navigation.extras.state['username'] || '';
      }

      // Carrega os registros (e busca o username se necessário)
      this.carregarRegistros();
    } else {
      this.controle_navegacao.navigateRoot('/login');
    }
  }

  async carregarRegistros() {
    const loading = await this.controle_carregamento.create({
      message: 'Carregando registros...',
      duration: 60000
    });
    await loading.present();

    if (!this.username) {
      await this.buscarUsername();
    }

    let url = `${environment.apiUrl}/usuarios/${this.usuario_id}/registros/`;

    // Adiciona filtro de tipo se não for 'todos'
    if (this.tipo_filtro !== 'todos') {
      url += `?tipo=${this.tipo_filtro}`;
    }

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: url
    };

    CapacitorHttp.get(options)
      .then((resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 200) {
          this.registros = resposta.data;
          this.registros_filtrados = this.registros;
        }
      })
      .catch((erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem('Erro ao carregar registros');
      });
  }

  async buscarUsername() {
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/usuarios/${this.usuario_id}/perfil/`
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.get(options);
      if (resposta.status == 200 && resposta.data.username) {
        this.username = resposta.data.username;
      }
    } catch (erro) {
      console.log('Erro ao buscar username:', erro);
      this.username = 'Usuário';
    }
  }

  filtrarPorTipo(tipo: string) {
    this.tipo_filtro = tipo;
    this.carregarRegistros();
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

  formatarData(data: string): string {
    const date = new Date(data);
    return date.toLocaleDateString('pt-BR');
  }

  async atualizar(event: any) {
    await this.carregarRegistros();
    event.target.complete();
  }

  async apresenta_mensagem(mensagem: string) {
    const toast = await this.controle_toast.create({
      message: mensagem,
      cssClass: 'ion-text-center',
      duration: 2000
    });
    toast.present();
  }

  voltar() {
    this.controle_navegacao.back();
  }
}
