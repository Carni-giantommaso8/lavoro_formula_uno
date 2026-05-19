import { TestBed } from '@angular/core/testing';

import { Scuderia } from './scuderia';

describe('Scuderia', () => {
  let service: Scuderia;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Scuderia);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
