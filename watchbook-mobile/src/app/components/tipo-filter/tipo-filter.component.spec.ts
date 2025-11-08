import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TipoFilterComponent } from './tipo-filter.component';

describe('TipoFilterComponent', () => {
  let component: TipoFilterComponent;
  let fixture: ComponentFixture<TipoFilterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TipoFilterComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(TipoFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
