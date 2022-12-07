<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">Waveshare Modbus RTU relay board to mqtt python interface</h3>

  <p align="center">
    Simple program to enable use of waveshare modbus rtu relay board with mqtt commands e.g. with home assistant.
    <br />
    <a href="https://github.com/linnukka/wavesharemodbusrturelaymqtt"><strong>Explore the docs »</strong></a>
    <br />
    <a href="https://github.com/linnukka/wavesharemodbusrturelaymqtt/issues">Report Bug</a>
    ·
    <a href="https://github.com/linnukka/wavesharemodbusrturelaymqtt/issues">Request Feature</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

<!-- 
* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->
<!-- GETTING STARTED -->
## Getting Started

1) Setup RS485 serial adapter and connect to Waveshare Modbus RTU relay board
2) Grant permissions to correct device eg. /dev/ttyUSB0 by adding user to dialout group 

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Required python libraries
  ```sh
  pip3 install pytz paho-mqtt configparser pymodbus pyserial
  ```
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/linnukka/wavesharemodbusrturelaymqtt.git
   ```
2. Tailor modbusrelay.conf and modbusrelay_logging.conf to your taste

3. Create mqtt_credentials.conf file to store username and password, see tags from the modbusrelay.conf file

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

Run modbusrelay.py to connect mqtt to modbus board:
  ```sh
  python3 modbusrelay.py
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- Create deamon files & examples
- Tidy up test script
- Create Home Assistant integration example

See the [open issues](https://github.com/linnukka/wavesharemodbusrturelaymqtt/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Juha - julli@iki.fi

Project Link: [https://github.com/linnukka/wavesharemodbusrturelaymqtt](https://github.com/linnukka/wavesharemodbusrturelaymqtt)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS
## Acknowledgments

* []()
* []()
* []()
 -->
 
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/linnukka/wavesharemodbusrturelaymqtt.svg?style=for-the-badge
[contributors-url]: https://github.com/linnukka/wavesharemodbusrturelaymqtt/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/linnukka/wavesharemodbusrturelaymqtt.svg?style=for-the-badge
[forks-url]: https://github.com/linnukka/wavesharemodbusrturelaymqtt/network/members
[stars-shield]: https://img.shields.io/github/stars/linnukka/wavesharemodbusrturelaymqtt.svg?style=for-the-badge
[stars-url]: https://github.com/linnukka/wavesharemodbusrturelaymqtt/stargazers
[issues-shield]: https://img.shields.io/github/issues/linnukka/wavesharemodbusrturelaymqtt.svg?style=for-the-badge
[issues-url]: https://github.com/linnukka/wavesharemodbusrturelaymqtt/issues
[license-shield]: https://img.shields.io/github/license/linnukka/wavesharemodbusrturelaymqtt.svg?style=for-the-badge
[license-url]: https://github.com/linnukka/wavesharemodbusrturelaymqtt/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 