import { Routes } from '@angular/router';
import { Scuderia } from './scuderia/scuderia';
import { SponsorComponent } from './sponsor/sponsor';

export const routes: Routes = [
    {path: 'scuderie', component: Scuderia},
    {path: 'sponsor', component: SponsorComponent},
    {path: '', redirectTo: '/scuderie', pathMatch: 'full'}
];