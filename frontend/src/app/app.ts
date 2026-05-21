import { Component, signal } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { Scuderia } from './scuderia/scuderia';
import { SponsorComponent } from './sponsor/sponsor';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Scuderia, SponsorComponent, RouterLink, RouterLinkActive],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}