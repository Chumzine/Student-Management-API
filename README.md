
<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Twitter][twitter-shield]][twitter-url]


<h3 align="center">Student Management API</h3>

  <p align="center">
    <a href="https://github.com/Chumzine/Student-Management-API"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Chumzine/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/Chumzine/repo_name/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About Student Management API</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#what-i-learnt">What I Learnt</a></li>
    <li>
      <a href="#how-to-use">How to Use</a>
      <ul>
        <li><a href="#sample">Sample</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About Student Management API

Student Management API, as the name implies, is a REST-API that allows schools create accounts for students and administrators to manage students data. It is hosted by the PythonAnywhere web hosting service and built with the Flask-RESTX framework. 

This project allows for CRUD operations, and comes with Swagger UI for easy testing and implementation. Also, administrators have full access, whereas students have limited access for some features and can only view some others with this application. 

Student Management API was built by <a href="https://github.com/Chumzine/">Chumzine</a>, with knowledge from the Backend Engineering live classes for Python by <a href="https://thealtschool.com/">AltSchool Africa</a>.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* ![Python][python]
* ![Flask][flask]
* ![SQLite][sqlite]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- What I Learnt from Building this Blog -->
## What I Learnt

This project helped me hone and practice my knowledge in the following:
* Python
* Flask-RESTX
* Routing
* Database Management
* Debugging
* Authentication
* Authorization
* API Development for Python
* API Deployment with PythonAnywhere
* Internet security

<p align="right"><a href="#readme-top">back to top</a></p>




<!-- HOW TO USE -->
## How to Use

To run this application, follow these steps:

1. Open this link on your browser, https://chumzine.pythonanywhere.com
   
2. Create an admin or student account;
   *To create an 'admin' account: Click on the 'auth' panel to open up a dropdown menu of routes, then click on the route that states 'Register a user'*
   *To create a 'student' account: Click on the 'user' panel to open up a dropdown menu of routes, then click on the route that states 'Create a student'*
   
3. Go to the 'Login' route on the 'auth' panel to generate a token for authorisation. Copy the token (without the quotation marks)
   
4. Scroll to the top of the page and click on the 'Authorize' tab on the right side. Paste the copied token in the 'Value' box, as such:
   ```sh
   Bearer <token>
   ```
   
5. Click on the 'Authorize' tab, then the 'Close' tab

6. You can now access any route, either as a student or an admin

7. Once you are done with the routes, scroll back up to the top and click on the 'Authorize' tab on the right side. Click on the 'Logout' tab


<!-- SAMPLE SCREENSHOTS -->
### Sample

<br />

[![Student Management API Screenshot 1][student-management-screenshot-1]](https://github.com/Chumzine/Student-Management-API/blob/master/images/Student_Management_API.png)

<br/>
<br />

[![Student Management API Screenshot 2][student-management-screenshot-2]](https://github.com/Chumzine/Student-Management-API/blob/master/images/Student_Management_API.png)

<br/>
<br />

[![Student Management API Screenshot 3][student-management-screenshot-3]](https://github.com/Chumzine/Student-Management-API/blob/master/images/Student_Management_API.png)

<br/>


<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- LICENSE -->
## License

Distributed under the MIT License. See <a href="https://github.com/Chumzine/Student-Management-API/blob/master/LICENSE">LICENSE</a> for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Adaobi Chuma-Okeke - [@twitter_handle](https://twitter.com/chumzine) - chumzine@gmail.com

Project Link: [https://github.com/Chumzine/Student-Management-API](https://github.com/Chumzine/Student-Management-API)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
* [Caleb Emelike's API, Flask and Database Lessons](https://github.com/CalebEmelike)
* [Dr. Austin Wopara](https://github.com/Ze-Austin/altschool-python)
* [Adeniyi Olanrewaju Mark](https://github.com/engrmarkk)
* [Stack Overflow](https://stackoverflow.com/)
* [Google](https://google.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Chumzine/Student-Management-API.svg?style=for-the-badge
[contributors-url]: https://github.com/Chumzine/Student-Management-API/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Chumzine/Student-Management-API.svg?style=for-the-badge
[forks-url]: https://github.com/Chumzine/Student-Management-API/network/members
[stars-shield]: https://img.shields.io/github/stars/Chumzine/Student-Management-API.svg?style=for-the-badge
[stars-url]: https://github.com/Chumzine/Student-Management-API/stargazers
[issues-shield]: https://img.shields.io/github/issues/Chumzine/Student-Management-API.svg?style=for-the-badge
[issues-url]: https://github.com/Chumzine/Student-Management-API/issues
[license-shield]: https://img.shields.io/github/license/Chumzine/Student-Management-API.svg?style=for-the-badge
[license-url]: https://github.com/Chumzine/Student-Management-API/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/she-adaobi-chuma-okeke-3677a9140
[twitter-shield]: https://img.shields.io/badge/-@chumzine-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/chumzine
[twitter-url]: https://twitter.com/chumzine
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
