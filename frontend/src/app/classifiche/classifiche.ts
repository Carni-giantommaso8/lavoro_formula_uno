import { Component, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClassificaService } from './classifiche.service';

@Component({
  selector: 'app-classifica',
  imports: [CommonModule],
  templateUrl: './classifiche.html',
  styleUrl: './classifiche.css'
})
export class ClassificaComponent implements OnInit {
  classificaPiloti = signal<any[]>([]);
  classificaCostruttori = signal<any[]>([]);

  constructor(private classificaService: ClassificaService) {}

  ngOnInit() {
    this.caricaClassificaPiloti();
    this.caricaClassificaCostruttori();
  }

  caricaClassificaPiloti() {
    this.classificaService.getClassificaPiloti().subscribe((data: any) => {
      this.classificaPiloti.set(data);
    });
  }

  caricaClassificaCostruttori() {
    this.classificaService.getClassificaCostruttori().subscribe((data: any) => {
      this.classificaCostruttori.set(data);
    });
  }
}