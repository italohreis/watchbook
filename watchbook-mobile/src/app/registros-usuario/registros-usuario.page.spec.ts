import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RegistrosUsuarioPage } from './registros-usuario.page';

describe('RegistrosUsuarioPage', () => {
  let component: RegistrosUsuarioPage;
  let fixture: ComponentFixture<RegistrosUsuarioPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(RegistrosUsuarioPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
