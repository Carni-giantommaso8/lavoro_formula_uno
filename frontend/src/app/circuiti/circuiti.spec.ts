import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CircuitiComponent } from './circuiti';

describe('CircuitiComponent', () => {
  let component: CircuitiComponent;
  let fixture: ComponentFixture<CircuitiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CircuitiComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(CircuitiComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});