import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ModalEditarRegistroComponent } from './modal-editar-registro.component';

describe('ModalEditarRegistroComponent', () => {
  let component: ModalEditarRegistroComponent;
  let fixture: ComponentFixture<ModalEditarRegistroComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalEditarRegistroComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(ModalEditarRegistroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
