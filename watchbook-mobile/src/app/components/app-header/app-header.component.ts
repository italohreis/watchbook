import { Component, Input } from '@angular/core';
import { IonHeader, IonToolbar, IonTitle } from '@ionic/angular/standalone';

@Component({
  selector: 'app-header',
  templateUrl: './app-header.component.html',
  styleUrls: ['./app-header.component.scss'],
  standalone: true,
  imports: [IonHeader, IonToolbar, IonTitle]
})
export class AppHeaderComponent {
  @Input() pageTitle: string = '';
}
