import { Injectable, computed, signal } from '@angular/core';

export interface Kazi {
  id: number;
  jina: string;
  imekamilika: boolean;
}

export type Kichujio = 'zote' | 'kamili' | 'haijamalizika';

@Injectable({ providedIn: 'root' })
export class KaziService {
  private readonly _kazi = signal<Kazi[]>([
    { id: 1, jina: 'Soma somo la Angular', imekamilika: true },
    { id: 2, jina: 'Andika component ya kwanza', imekamilika: false },
    { id: 3, jina: 'Endesha `ng serve`', imekamilika: false },
  ]);

  readonly kazi = this._kazi.asReadonly();
  readonly kamili = computed(() => this._kazi().filter(k => k.imekamilika).length);
  readonly haijamalizika = computed(() => this._kazi().filter(k => !k.imekamilika).length);

  idhini(id: number): void {
    this._kazi.update(list =>
      list.map(k => (k.id === id ? { ...k, imekamilika: !k.imekamilika } : k))
    );
  }

  ongeza(jina: string): void {
    const jinaSafi = jina.trim();
    if (!jinaSafi) {
      return;
    }
    this._kazi.update(list => [
      ...list,
      {
        id: Math.max(0, ...list.map(k => k.id)) + 1,
        jina: jinaSafi,
        imekamilika: false,
      },
    ]);
  }
}
