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
  AlertController,
  IonText,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonList,
  IonItem,
  IonLabel,
  IonButton,
  IonButtons,
  IonIcon,
  IonBadge,
  IonSearchbar,
  IonRefresher,
  IonRefresherContent
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Usuario } from '../login/models/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppHeaderComponent } from '../components/app-header/app-header.component';
import { environment } from '../../environments/environment';
import { addIcons } from 'ionicons';
import {
  personAddOutline,
  personRemoveOutline,
  searchOutline,
  checkmarkCircle,
  closeCircle,
  timeOutline,
  peopleOutline
} from 'ionicons/icons';

interface Amizade {
  id: number;
  de_usuario: {
    id: number;
    username: string;
    first_name: string;
  };
  para_usuario: {
    id: number;
    username: string;
    first_name: string;
  };
  status: string;
  status_display: string;
  data_criacao: string;
}

interface UsuarioBusca {
  id: number;
  username: string;
  first_name: string;
  email: string;
}

@Component({
  selector: 'app-amigos',
  templateUrl: './amigos.page.html',
  styleUrls: ['./amigos.page.scss'],
  standalone: true,
  imports: [
    AppHeaderComponent,
    IonContent,
    CommonModule,
    FormsModule,
    IonHeader,
    IonTitle,
    IonToolbar,
    IonText,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonList,
    IonItem,
    IonLabel,
    IonButton,
    IonButtons,
    IonIcon,
    IonBadge,
    IonSearchbar,
    IonRefresher,
    IonRefresherContent
  ],
  providers: [Storage]
})
export class AmigosPage implements OnInit {
  usuario: Usuario = new Usuario();
  pedidos_pendentes: Amizade[] = [];
  todas_amizades: Amizade[] = [];
  amigos: Amizade[] = [];
  usuarios_busca: UsuarioBusca[] = [];
  termo_busca: string = '';
  mostrar_resultados: boolean = false;

  constructor(
    private storage: Storage,
    private controle_toast: ToastController,
    private controle_navegacao: NavController,
    private controle_carregamento: LoadingController,
    private controle_alerta: AlertController
  ) {
    addIcons({
      personAddOutline,
      personRemoveOutline,
      searchOutline,
      checkmarkCircle,
      closeCircle,
      timeOutline,
      peopleOutline
    });
  }

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.carregarTodasAmizades();
      this.carregarPedidosPendentes();
      this.carregarAmigos();
    } else {
      this.controle_navegacao.navigateRoot('/login');
    }
  }

  async carregarTodasAmizades() {
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/amizades/`
    };

    CapacitorHttp.get(options)
      .then((resposta: HttpResponse) => {
        if (resposta.status == 200) {
          this.todas_amizades = resposta.data;
        }
      })
      .catch((erro: any) => {
        console.log(erro);
      });
  }

  async carregarPedidosPendentes() {
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/amizades/pendentes/`
    };

    CapacitorHttp.get(options)
      .then((resposta: HttpResponse) => {
        if (resposta.status == 200) {
          this.pedidos_pendentes = resposta.data;
        }
      })
      .catch((erro: any) => {
        console.log(erro);
      });
  }

  async carregarAmigos() {
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/amizades/aceitas/`
    };

    CapacitorHttp.get(options)
      .then((resposta: HttpResponse) => {
        if (resposta.status == 200) {
          this.amigos = resposta.data;
        }
      })
      .catch((erro: any) => {
        console.log(erro);
      });
  }

  async buscarUsuarios() {
    if (!this.termo_busca.trim()) {
      this.apresenta_mensagem('Digite um nome para buscar');
      return;
    }

    const loading = await this.controle_carregamento.create({
      message: 'Buscando usuários...',
      duration: 60000
    });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/usuarios/?search=${encodeURIComponent(this.termo_busca)}`
    };

    CapacitorHttp.get(options)
      .then((resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 200) {
          // Filtra o próprio usuário da lista
          this.usuarios_busca = resposta.data.filter((u: UsuarioBusca) => u.id !== this.usuario.id);
          this.mostrar_resultados = true;
        }
      })
      .catch((erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem('Erro ao buscar usuários');
      });
  }

  async enviarPedido(usuario_id: number) {
    const loading = await this.controle_carregamento.create({
      message: 'Enviando solicitação...',
      duration: 60000
    });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/amizades/`,
      data: {
        para_usuario: usuario_id
      }
    };

    CapacitorHttp.post(options)
      .then((resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 201 || resposta.status == 200) {
          this.apresenta_mensagem('Solicitação enviada com sucesso!');
          this.carregarTodasAmizades(); // Atualiza todas as amizades
          this.buscarUsuarios(); // Atualiza a lista
        } else {
          const mensagem = resposta.data?.para_usuario?.[0] || 'Erro ao enviar solicitação';
          this.apresenta_mensagem(mensagem);
        }
      })
      .catch((erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem('Erro ao enviar solicitação');
      });
  }

  async aceitarPedido(pedido_id: number) {
    const loading = await this.controle_carregamento.create({
      message: 'Aceitando solicitação...',
      duration: 60000
    });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/amizades/${pedido_id}/aceitar/`
    };

    CapacitorHttp.post(options)
      .then((resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 200) {
          this.apresenta_mensagem('Solicitação aceita!');
          this.carregarTodasAmizades();
          this.carregarPedidosPendentes();
          this.carregarAmigos();
        }
      })
      .catch((erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem('Erro ao aceitar solicitação');
      });
  }

  async rejeitarPedido(pedido_id: number) {
    const loading = await this.controle_carregamento.create({
      message: 'Rejeitando solicitação...',
      duration: 60000
    });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/amizades/${pedido_id}/rejeitar/`
    };

    CapacitorHttp.post(options)
      .then((resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 204 || resposta.status == 200) {
          this.apresenta_mensagem('Solicitação rejeitada');
          this.carregarPedidosPendentes();
        }
      })
      .catch((erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem('Erro ao rejeitar solicitação');
      });
  }

  async confirmarRemoverAmigo(amizade: Amizade) {
    const amigo = amizade.de_usuario.id === this.usuario.id 
      ? amizade.para_usuario 
      : amizade.de_usuario;

    const alert = await this.controle_alerta.create({
      header: 'Confirmar Remoção',
      message: `Deseja remover <strong>${amigo.username}</strong> da sua lista de amigos?`,
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel'
        },
        {
          text: 'Remover',
          role: 'confirm',
          handler: () => {
            this.removerAmigo(amizade.id);
          }
        }
      ]
    });

    await alert.present();
  }

  async removerAmigo(amizade_id: number) {
    const loading = await this.controle_carregamento.create({
      message: 'Removendo amigo...',
      duration: 60000
    });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${environment.apiUrl}/amizades/${amizade_id}/`
    };

    CapacitorHttp.delete(options)
      .then((resposta: HttpResponse) => {
        loading.dismiss();
        if (resposta.status == 204 || resposta.status == 200) {
          this.apresenta_mensagem('Amigo removido');
          this.carregarAmigos();
        }
      })
      .catch((erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem('Erro ao remover amigo');
      });
  }

  obterNomeAmigo(amizade: Amizade): string {
    if (amizade.de_usuario.id === this.usuario.id) {
      return amizade.para_usuario.first_name || amizade.para_usuario.username;
    } else {
      return amizade.de_usuario.first_name || amizade.de_usuario.username;
    }
  }

  obterUsernameAmigo(amizade: Amizade): string {
    if (amizade.de_usuario.id === this.usuario.id) {
      return amizade.para_usuario.username;
    } else {
      return amizade.de_usuario.username;
    }
  }

  verificarStatusAmizade(usuario_id: number): string {
    // Verifica se já é amigo (status ACEITO)
    const jaAmigo = this.todas_amizades.find(a => 
      a.status === 'ACEITO' && 
      (a.de_usuario.id === usuario_id || a.para_usuario.id === usuario_id)
    );
    if (jaAmigo) return 'ACEITO';

    // Verifica se tem pedido pendente enviado (eu enviei para ele)
    const pedidoEnviado = this.todas_amizades.find(a => 
      a.status === 'PENDENTE' &&
      a.de_usuario.id === this.usuario.id && 
      a.para_usuario.id === usuario_id
    );
    if (pedidoEnviado) return 'PENDENTE_ENVIADO';

    // Verifica se tem pedido pendente recebido (ele enviou para mim)
    const pedidoRecebido = this.todas_amizades.find(a => 
      a.status === 'PENDENTE' &&
      a.de_usuario.id === usuario_id && 
      a.para_usuario.id === this.usuario.id
    );
    if (pedidoRecebido) return 'PENDENTE_RECEBIDO';

    return 'NENHUM';
  }

  async atualizar(event: any) {
    await this.carregarTodasAmizades();
    await this.carregarPedidosPendentes();
    await this.carregarAmigos();
    if (this.mostrar_resultados && this.termo_busca) {
      await this.buscarUsuarios();
    }
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
}
