import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassificaComponent } from './classifiche';

describe('ClassificaComponent', () => {
  let component: ClassificaComponent;
  let fixture: ComponentFixture<ClassificaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassificaComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ClassificaComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});