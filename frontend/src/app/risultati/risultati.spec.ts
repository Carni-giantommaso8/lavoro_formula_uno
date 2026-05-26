import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Risultati } from './risultati';

describe('Risultati', () => {
  let component: Risultati;
  let fixture: ComponentFixture<Risultati>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Risultati],
    }).compileComponents();

    fixture = TestBed.createComponent(Risultati);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
