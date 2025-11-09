import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ModalAdicionarRegistroComponent } from './modal-adicionar-registro.component';

describe('ModalAdicionarRegistroComponent', () => {
  let component: ModalAdicionarRegistroComponent;
  let fixture: ComponentFixture<ModalAdicionarRegistroComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModalAdicionarRegistroComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(ModalAdicionarRegistroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
