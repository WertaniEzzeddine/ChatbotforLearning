import { Component, OnDestroy, OnInit } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { Subscription } from 'rxjs';
@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit, OnDestroy {
  user:any;
  booleanValue:boolean =false;
  private subscription!: Subscription;

  constructor(private authService:AuthService){};

  logout(){
    this.booleanValue=false;
    this.authService.setBooleanValue(false);
    localStorage.removeItem('userToken');

  }
  ngOnInit(): void {
    this.subscription = this.authService.boolean$.subscribe((status) => {
      this.booleanValue = status;
      console.log('Login status changed:', status);
    });
 
}
ngOnDestroy() {
  // Unsubscribe to prevent memory leaks
  if (this.subscription) {
    this.subscription.unsubscribe();
  }
}

}
