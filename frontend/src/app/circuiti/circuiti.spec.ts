import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Circuiti } from './circuiti';

describe('Circuiti', () => {
  let component: Circuiti;
  let fixture: ComponentFixture<Circuiti>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Circuiti],
    }).compileComponents();

    fixture = TestBed.createComponent(Circuiti);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
