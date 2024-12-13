import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router'; // To navigate after successful registration

@Component({
  selector: 'app-singup',
  templateUrl: './singup.component.html',
  styleUrls: ['./singup.component.scss']
})
export class SingupComponent {
  user = { full_name: '', email: '', password: '' };  // Bind the user data

  constructor(private authService: AuthService, private router: Router) {}

  // Handle form submission
  onSubmit() {
    const { full_name, email, password } = this.user;
    const userData = { full_name, email, password };

    // Call the register API
    this.authService.registerUser(userData).subscribe({
      next: (response) => {
       
        console.log(response);
        
        this.router.navigate(['/login']);  // Redirect to login page after successful registration
      },
      error: (err) => {
        alert('Registration failed!');
        console.error(err);
      }
    });
  }
}
