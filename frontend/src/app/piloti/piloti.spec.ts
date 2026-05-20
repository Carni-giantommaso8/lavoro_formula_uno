import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PilotiComponent } from './piloti';

describe('PilotiComponent', () => {
  let component: PilotiComponent;
  let fixture: ComponentFixture<PilotiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PilotiComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(PilotiComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});