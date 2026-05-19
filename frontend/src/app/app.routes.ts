import { Routes } from '@angular/router';
import { ScuderiaComponent } from './scuderia/scuderia';

export const routes: Routes = [
    { path: 'scuderia', component: ScuderiaComponent },
    {path: '', redirectTo: '/scuderia', pathMatch: 'full'},
];

