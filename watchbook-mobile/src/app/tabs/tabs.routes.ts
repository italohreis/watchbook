import { Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

export const routes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      {
        path: 'inicio',
        loadComponent: () =>
          import('../inicio/inicio.page').then((m) => m.InicioPage),
      },
      {
        path: 'obras',
        loadComponent: () =>
          import('../catalogo/catalogo.page').then((m) => m.CatalogoPage),
      },
      {
        path: 'registros',
        loadComponent: () =>
          import('../registros/registros.page').then((m) => m.RegistrosPage),
      },
      {
        path: 'amigos',
        loadComponent: () =>
          import('../amigos/amigos.page').then((m) => m.AmigosPage),
      },
      {
        path: 'perfil',
        loadComponent: () =>
          import('../perfil/perfil.page').then((m) => m.PerfilPage),
      },
      {
        path: '',
        redirectTo: 'inicio',
        pathMatch: 'full',
      },
    ],
  },
];
