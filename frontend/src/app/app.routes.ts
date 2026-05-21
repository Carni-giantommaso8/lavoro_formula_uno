import { Routes } from '@angular/router';
import { Scuderia } from './scuderia/scuderia';
import { SponsorComponent } from './sponsor/sponsor';
import {PilotiComponent} from './piloti/piloti';
import {ClassificaComponent} from './classifiche/classifiche';

export const routes: Routes = [
    {path: 'scuderie', component: Scuderia},
    {path: 'sponsor', component: SponsorComponent},
    {path: 'piloti', component: PilotiComponent},
    {path: 'classifiche', component: ClassificaComponent},
    {path: '', redirectTo: '/scuderie', pathMatch: 'full'}
];