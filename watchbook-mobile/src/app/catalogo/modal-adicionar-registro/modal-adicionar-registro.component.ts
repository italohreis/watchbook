import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonButton,
  IonContent,
  IonItem,
  IonLabel,
  IonTextarea,
  IonIcon,
  ModalController
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { closeOutline, star, starOutline } from 'ionicons/icons';

@Component({
  selector: 'app-modal-adicionar-registro',
  templateUrl: './modal-adicionar-registro.component.html',
  styleUrls: ['./modal-adicionar-registro.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonButton,
    IonContent,
    IonItem,
    IonLabel,
    IonTextarea,
    IonIcon
  ]
})
export class ModalAdicionarRegistroComponent {
  @Input() obra: any;

  public nota: number = 0;
  public critica: string = '';

  constructor(private modalController: ModalController) {
    addIcons({
      'close-outline': closeOutline,
      'star': star,
      'star-outline': starOutline
    });
  }

  fecharModal() {
    this.modalController.dismiss();
  }

  salvarRegistro() {
    const dados = {
      obra: this.obra.id,
      nota: this.nota,
      critica: this.critica
    };
    this.modalController.dismiss(dados, 'salvar');
  }

  selecionarNota(nota: number) {
    this.nota = nota;
  }

  gerarEstrelas(): number[] {
    return [1, 2, 3, 4, 5];
  }
}
