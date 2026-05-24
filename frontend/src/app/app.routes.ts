import { Routes } from '@angular/router';
import { Scuderia } from './scuderia/scuderia';
import { SponsorComponent } from './sponsor/sponsor';
import {PilotiComponent} from './piloti/piloti';
import {ClassificheComponent} from './classifiche/classifiche';
import {CircuitiComponent} from './circuiti/circuiti';

export const routes: Routes = [
    {path: 'scuderie', component: Scuderia},
    {path: 'sponsor', component: SponsorComponent},
    {path: 'piloti', component: PilotiComponent},
    {path: 'classifiche', component: ClassificheComponent},
    {path: 'circuiti', component: CircuitiComponent},
    {path: '', redirectTo: '/scuderie', pathMatch: 'full'}
];