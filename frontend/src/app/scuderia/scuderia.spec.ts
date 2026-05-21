import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Scuderia } from './scuderia';

describe('Scuderia', () => {
  let component: Scuderia;
  let fixture: ComponentFixture<Scuderia>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Scuderia],
    }).compileComponents();

    fixture = TestBed.createComponent(Scuderia);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});