import { Component, Input, OnInit } from '@angular/core';
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
  IonInput,
  IonTextarea,
  IonIcon,
  ModalController
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { closeOutline, star, starOutline } from 'ionicons/icons';

@Component({
  selector: 'app-modal-editar-registro',
  templateUrl: './modal-editar-registro.component.html',
  styleUrls: ['./modal-editar-registro.component.scss'],
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
    IonInput,
    IonTextarea,
    IonIcon
  ]
})
export class ModalEditarRegistroComponent implements OnInit {
  @Input() registro: any;

  public nota: number = 0;
  public critica: string = '';
  public data_assistido: string = '';

  constructor(private modalController: ModalController) {
    addIcons({
      'close-outline': closeOutline,
      'star': star,
      'star-outline': starOutline
    });
  }

  ngOnInit() {
    if (this.registro) {
      this.nota = this.registro.nota || 0;
      this.critica = this.registro.critica || '';
      this.data_assistido = this.registro.data_assistido || '';
    }
  }

  fecharModal() {
    this.modalController.dismiss();
  }

  salvarEdicao() {
    const dados = {
      nota: this.nota,
      critica: this.critica,
      data_assistido: this.data_assistido
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
