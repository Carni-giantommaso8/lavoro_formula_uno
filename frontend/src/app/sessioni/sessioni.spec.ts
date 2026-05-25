import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Sessioni } from './sessioni';

describe('Sessioni', () => {
  let component: Sessioni;
  let fixture: ComponentFixture<Sessioni>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Sessioni],
    }).compileComponents();

    fixture = TestBed.createComponent(Sessioni);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
