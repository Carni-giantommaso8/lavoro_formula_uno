import { Routes } from '@angular/router';
import { Scuderia } from './scuderia/scuderia';
import { SponsorComponent } from './sponsor/sponsor';
import { PilotiComponent } from './piloti/piloti';
import { CircuitiComponent } from './circuiti/circuiti';
import { GranPremiComponent } from './gran-premi/gran-premi';
import { SessioniComponent } from './sessioni/sessioni';
import { RisultatiComponent } from './risultati/risultati';
 
export const routes: Routes = [
  { path: 'scuderie',    component: Scuderia },
  { path: 'sponsor',     component: SponsorComponent },
  { path: 'piloti',      component: PilotiComponent },
  { path: 'circuiti',    component: CircuitiComponent },
  { path: 'gran-premi',  component: GranPremiComponent },
  { path: 'sessioni',    component: SessioniComponent },
  { path: 'risultati',   component: RisultatiComponent },
  { path: '',            redirectTo: '/scuderie', pathMatch: 'full' }
];
 
