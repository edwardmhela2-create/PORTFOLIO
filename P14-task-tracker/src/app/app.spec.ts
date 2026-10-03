import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should render title', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Fuatilia Kazi');
  });

  it('kazi zilizomo = 3 na zilizokamilika = 1', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app['kazi']().length).toBe(3);
    expect(app['kamiliZilizo']()).toBe(1);
  });

  it('badiliza inabadilisha hali ya kazi', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    app['badiliza'](2);
    expect(app['kamiliZilizo']()).toBe(2);
    app['badiliza'](2);
    expect(app['kamiliZilizo']()).toBe(1);
  });
});
