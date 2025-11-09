import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent,
  IonLabel,
  IonInput,
  IonItem,
  IonButton,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonText
} from '@ionic/angular/standalone';
import { LoadingController } from '@ionic/angular';
import { NavController } from '@ionic/angular';
import { ToastController } from '@ionic/angular';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppHeaderComponent } from '../components/app-header/app-header.component';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-cadastro',
  templateUrl: './cadastro.page.html',
  styleUrls: ['./cadastro.page.scss'],
  standalone: true,
  imports: [
    AppHeaderComponent,
    IonContent,
    CommonModule,
    FormsModule,
    IonLabel,
    IonInput,
    IonItem,
    IonButton,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle,
    IonText
  ]
})
export class CadastroPage implements OnInit {
  primeiro_nome: string = '';
  nome_usuario: string = '';
  senha: string = '';
  confirmacao_senha: string = '';

  constructor(
    private controle_carregamento: LoadingController,
    private controle_navegacao: NavController,
    private controle_toast: ToastController
  ) {
  }

  ngOnInit() {}

  async cadastrarUsuario() {
    // Validações básicas
    if (!this.primeiro_nome.trim()) {
      this.apresenta_mensagem('Por favor, informe seu nome');
      return;
    }

    if (!this.nome_usuario.trim()) {
      this.apresenta_mensagem('Por favor, informe um nome de usuário');
      return;
    }

    if (this.nome_usuario.length < 3) {
      this.apresenta_mensagem('Nome de usuário deve ter pelo menos 3 caracteres');
      return;
    }

    if (!this.senha) {
      this.apresenta_mensagem('Por favor, informe uma senha');
      return;
    }

    if (this.senha.length < 6) {
      this.apresenta_mensagem('A senha deve ter pelo menos 6 caracteres');
      return;
    }

    if (this.senha !== this.confirmacao_senha) {
      this.apresenta_mensagem('As senhas não conferem');
      return;
    }

    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({
      message: 'Criando sua conta...',
      duration: 15000
    });
    await loading.present();

    // Define informações da requisição
    const options: HttpOptions = {
      headers: { 'Content-Type': 'application/json' },
      url: `${environment.apiUrl}/usuarios/`,
      data: {
        first_name: this.primeiro_nome,
        username: this.nome_usuario,
        password: this.senha,
        password2: this.confirmacao_senha
      }
    };

    // Cria usuário na API
    CapacitorHttp.post(options)
      .then(async (resposta: HttpResponse) => {
        loading.dismiss();

        // Verifica se a requisição foi processada com sucesso
        if (resposta.status == 201 || resposta.status == 200) {
          this.apresenta_mensagem('Conta criada com sucesso! Faça login para continuar.');
          // Redireciona para tela de login
          setTimeout(() => {
            this.controle_navegacao.navigateRoot('/login');
          }, 1500);
        } else {
          // Trata erros de validação
          let mensagem_erro = 'Não foi possível criar a conta. ';
          
          if (resposta.data?.username) {
            mensagem_erro += resposta.data.username[0];
          } else if (resposta.data?.password) {
            mensagem_erro += resposta.data.password[0];
          } else if (resposta.data?.password2) {
            mensagem_erro += resposta.data.password2[0];
          } else {
            mensagem_erro += 'Verifique os dados e tente novamente.';
          }
          
          this.apresenta_mensagem(mensagem_erro);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        
        let mensagem_erro = 'Erro ao criar conta: ';
        if (erro.message) {
          mensagem_erro += erro.message;
        } else {
          mensagem_erro += 'Verifique sua conexão e tente novamente.';
        }
        
        this.apresenta_mensagem(mensagem_erro);
      });
  }

  voltarParaLogin() {
    this.controle_navegacao.navigateBack('/login');
  }

  async apresenta_mensagem(mensagem: string) {
    const toast = await this.controle_toast.create({
      message: mensagem,
      cssClass: 'ion-text-center',
      duration: 3000
    });
    toast.present();
  }
}
