import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonSegment,
  IonSegmentButton,
  IonIcon,
  IonLabel
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { gridOutline, filmOutline, tvOutline } from 'ionicons/icons';

@Component({
  selector: 'app-tipo-filter',
  templateUrl: './tipo-filter.component.html',
  styleUrls: ['./tipo-filter.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonSegment,
    IonSegmentButton,
    IonIcon,
    IonLabel
  ]
})
export class TipoFilterComponent {
  @Input() value: string = 'todos';
  @Output() valueChange = new EventEmitter<string>();

  constructor() {
    addIcons({
      'grid-outline': gridOutline,
      'film-outline': filmOutline,
      'tv-outline': tvOutline
    });
  }

  onFilterChange(event: any) {
    const newValue = event.detail.value;
    this.value = newValue;
    this.valueChange.emit(newValue);
  }
}
