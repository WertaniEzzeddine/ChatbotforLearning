import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  constructor(private authService:AuthService, private router: Router){};
  user = { email: '', password: '' };
  us = {id:0, full_name: '', email: '' };
  
  onSubmit() {
    const { email, password } = this.user;
    const userData = { email, password };


    // Call the register API
    this.authService.loginUser(userData).subscribe({
      next: (response) => {
        this.us=response.user;
        this.authService.setUser(this.us);
        console.log(this.authService.user)
        this.authService.setBooleanValue(true);
        
        console.log(response);
        localStorage.setItem('userToken', response.access_token);
        this.router.navigate(['/chat']);  // Redirect to login page after successful registration
      },
      error: (err) => {
        alert('login failed!');
        console.error(err);
      }
    });
  }

}
