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
  ModalController,
  IonText,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonCardContent,
  IonItem,
  IonThumbnail,
  IonLabel,
  IonIcon,
  IonBadge,
  IonButton,
  IonButtons,
  IonGrid,
  IonRow,
  IonCol,
  IonItemSliding,
  IonItemOptions,
  IonItemOption,
  AlertController
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Usuario } from '../login/models/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppHeaderComponent } from '../components/app-header/app-header.component';
import { ModalEditarRegistroComponent } from './modal-editar-registro/modal-editar-registro.component';
import { TipoFilterComponent } from '../components/tipo-filter/tipo-filter.component';
import { environment } from '../../environments/environment';
import { addIcons } from 'ionicons';
import {
  starOutline,
  star,
  calendarOutline,
  filmOutline,
  tvOutline,
  gridOutline,
  trashOutline,
  createOutline
} from 'ionicons/icons';

export interface RegistroAssistido {
  id: number;
  obra: {
    id: number;
    titulo: string;
    ano_lancamento: number;
    diretor: string;
    genero: string;
    poster: string;
    tipo: string;
    tipo_display: string;
  };
  nota: number;
  critica: string;
  data_assistido: string;
}

@Component({
  standalone: true,
  selector: 'app-registros',
  templateUrl: './registros.page.html',
  styleUrls: ['./registros.page.scss'],
  imports: [
    AppHeaderComponent,
    TipoFilterComponent,
    IonItemOption,
    IonItemOptions,
    IonItemSliding,
    IonCol,
    IonRow,
    IonGrid,
    IonButtons,
    IonButton,
    IonBadge,
    IonLabel,
    IonItem,
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
export class RegistrosPage implements OnInit {

  public usuario: Usuario = new Usuario();
  public registros: RegistroAssistido[] = [];
  public registros_filtrados: RegistroAssistido[] = [];
  public tipo_filtro: string = 'todos';

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    public controle_alerta: AlertController,
    public controle_modal: ModalController
  ) {
    addIcons({
      'star-outline': starOutline,
      'star': star,
      'calendar-outline': calendarOutline,
      'film-outline': filmOutline,
      'tv-outline': tvOutline,
      'grid-outline': gridOutline,
      'trash-outline': trashOutline,
      'create-outline': createOutline
    });
  }

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
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

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/registros/`
    };

    CapacitorHttp.get(options)
      .then(async (resposta: HttpResponse) => {
        if (resposta.status == 200) {
          this.registros = resposta.data;
          this.aplicarFiltro();
          loading.dismiss();
        } else {
          loading.dismiss();
          this.apresenta_mensagem(`Falha ao carregar registros: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao carregar registros: ${erro?.message || 'Erro desconhecido'}`);
      });
  }

  filtrarPorTipo(event: any) {
    this.tipo_filtro = event;
    this.aplicarFiltro();
  }

  aplicarFiltro() {
    if (this.tipo_filtro === 'todos') {
      this.registros_filtrados = [...this.registros];
    } else {
      this.registros_filtrados = this.registros.filter(
        r => r.obra.tipo.toLowerCase() === this.tipo_filtro.toLowerCase()
      );
    }
  }

  async confirmarExclusao(registro: RegistroAssistido) {
    const alert = await this.controle_alerta.create({
      header: 'Confirmar Exclusão',
      message: `Deseja realmente excluir o registro de "${registro.obra.titulo}"?`,
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel'
        },
        {
          text: 'Excluir',
          role: 'destructive',
          handler: () => {
            this.excluirRegistro(registro.id);
          }
        }
      ]
    });

    await alert.present();
  }

  async excluirRegistro(id: number) {
    const loading = await this.controle_carregamento.create({
      message: 'Excluindo...',
      duration: 60000
    });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/registros/${id}/`
    };

    CapacitorHttp.delete(options)
      .then(async (resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 204 || resposta.status == 200) {
          this.apresenta_mensagem('Registro excluído com sucesso!');
          this.carregarRegistros();
        } else {
          this.apresenta_mensagem(`Falha ao excluir: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao excluir: ${erro?.message || 'Erro desconhecido'}`);
      });
  }

  async abrirModalEdicao(registro: RegistroAssistido) {
    const modal = await this.controle_modal.create({
      component: ModalEditarRegistroComponent,
      componentProps: {
        registro: registro
      }
    });

    modal.present();

    const { data, role } = await modal.onWillDismiss();

    if (role === 'salvar' && data) {
      this.editarRegistro(registro.id, data);
    }
  }

  async editarRegistro(id: number, dados: any) {
    const loading = await this.controle_carregamento.create({
      message: 'Salvando alterações...',
      duration: 60000
    });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/registros/${id}/`,
      data: dados
    };

    CapacitorHttp.patch(options)
      .then(async (resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 200) {
          this.apresenta_mensagem('Registro atualizado com sucesso!');
          this.carregarRegistros();
        } else {
          this.apresenta_mensagem(`Falha ao atualizar: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao atualizar: ${erro?.message || 'Erro desconhecido'}`);
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

  gerarEstrelas(nota: number): boolean[] {
    return Array(5).fill(false).map((_, i) => i < nota);
  }

  formatarData(data: string): string {
    const date = new Date(data);
    return date.toLocaleDateString('pt-BR');
  }
}
