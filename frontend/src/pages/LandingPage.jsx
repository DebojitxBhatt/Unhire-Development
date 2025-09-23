import React from "react";

const LandingPage = () => {
  return (
    <div
      className="relative flex size-full min-h-screen flex-col overflow-x-hidden bg-gray-50"
      style={{ fontFamily: 'Manrope, "Noto Sans", sans-serif' }}
    >
      {/* Header */}
      <header className="flex items-center justify-between border-b border-gray-200 px-10 py-4 bg-white">
        <div className="flex items-center gap-3 text-gray-900">
          <div className="size-6 text-[#87CEEB]">
            <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <path
                clipRule="evenodd"
                d="M12.0799 24L4 19.2479L9.95537 8.75216L18.04 13.4961L18.0446 4H29.9554L29.96 13.4961L38.0446 8.75216L44 19.2479L35.92 24L44 28.7521L38.0446 39.2479L29.96 34.5039L29.9554 44H18.0446L18.04 34.5039L9.95537 39.2479L4 28.7521L12.0799 24Z"
                fill="currentColor"
                fillRule="evenodd"
              ></path>
            </svg>
          </div>
          <h2 className="text-xl font-bold">Unhire</h2>
        </div>
        <div className="flex flex-1 justify-end gap-4">
          <nav className="flex items-center gap-6">
            <a href="#" className="text-sm font-medium text-gray-700 hover:text-gray-900">
              Find Work
            </a>
            <a href="#" className="text-sm font-medium text-gray-700 hover:text-gray-900">
              Find Talent
            </a>
            <a href="#" className="text-sm font-medium text-gray-700 hover:text-gray-900">
              Why Unhire?
            </a>
            <a href="#" className="text-sm font-medium text-gray-700 hover:text-gray-900">
              Pricing
            </a>
          </nav>
          <div className="flex gap-3">
            <button className="h-10 px-5 rounded-lg bg-gradient-to-br from-[#87CEEB] to-[#AFEEEE] text-white text-sm font-bold shadow-sm hover:from-[#AFEEEE] hover:to-[#87CEEB] transition transform hover:scale-105">
              Post a Job
            </button>
            <button className="h-10 px-5 rounded-lg bg-gray-100 text-gray-800 text-sm font-bold hover:bg-gray-200 transition transform hover:scale-105">
              Log In
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1">
        <div className="px-40 flex justify-center py-20 bg-white">
          <div className="max-w-5xl flex-1">
            <div className="p-4">
              <div
                className="flex min-h-[480px] flex-col gap-8 rounded-2xl bg-cover bg-center bg-no-repeat items-start justify-end px-12 pb-12"
                style={{
                  backgroundImage:
                    'linear-gradient(to top, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.1) 50%, rgba(0,0,0,0) 100%), url("https://lh3.googleusercontent.com/aida-public/AB6AXuDgdNAC7bzVkKikk-7R4RPzpKs4WbV7ducOXOnuMu7DQXNP40rxqZonXiFJGaYcmIQ-Ffmgy--qK4jSBLpLTqnEzeU82ggfgeGrWtqLM24fkuhmQ1qvei--Bupiy19lsOPCz2sB44EjyYrCmZ49sgBNw5Fw3DGS7i_MEDQRnrrRPOleK-TETJ_YH1ZIAApQc5d67QjR1RbGVGENCB8yH3K7N-yoD6mh_B0dirDjyB0kny_sp-RP_qFTkXc_cAW5Hqlv1u2IkJ9MSiZo")',
                }}
              >
                <div className="flex flex-col gap-4 text-left max-w-2xl">
                  <h1 className="text-white text-5xl font-extrabold leading-tight tracking-tighter">
                    Find the perfect freelancer for your project
                  </h1>
                  <h2 className="text-gray-200 text-lg">
                    Connect with top-tier talent and get your work done efficiently. Post a job or browse available freelancers to start collaborating.
                  </h2>
                </div>
                <div className="flex gap-4 mt-4">
                  <button className="h-12 px-6 rounded-xl bg-gradient-to-br from-[#87CEEB] to-[#AFEEEE] text-white text-base font-bold shadow-lg hover:from-[#AFEEEE] hover:to-[#87CEEB] transition transform hover:scale-105">
                    Hire instantly
                  </button>
                  <button className="h-12 px-6 rounded-xl bg-[#F08080] text-white text-base font-bold shadow-lg hover:bg-opacity-90 transition transform hover:scale-105">
                    Work instantly
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* How Unhire Works Section */}
        <section className="flex flex-col gap-16 px-4 py-20 bg-white text-center">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tighter">How Unhire Works</h1>
            <p className="text-gray-600 text-lg">
              Our platform connects you with skilled freelancers for both short-term tasks and long-term collaborations.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Card 1 */}
            <div className="flex flex-col gap-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm hover:shadow-lg transition">
              <div className="text-[#87CEEB]">
                <svg fill="currentColor" viewBox="0 0 256 256" width="32" height="32">
                  <path d="M216,56H176V48a24,24,0,0,0-24-24H104A24,24,0,0,0,80,48v8H40A16,16,0,0,0,24,72V200a16,16,0,0,0,16,16H216a16,16,0,0,0,16-16V72A16,16,0,0,0,216,56ZM96,48a8,8,0,0,1,8-8h48a8,8,0,0,1,8,8v8H96Zm120,152H40V131.64A200.19,200.19,0,0,0,128,152a200.25,200.25,0,0,0,88-20.37V200Z"></path>
                </svg>
              </div>
              <h2 className="text-lg font-bold">Post a Job</h2>
              <p className="text-sm text-gray-500">
                Describe your project and requirements to attract qualified freelancers.
              </p>
            </div>
            {/* Card 2 */}
            <div className="flex flex-col gap-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm hover:shadow-lg transition">
              <div className="text-[#87CEEB]">
                <svg fill="currentColor" viewBox="0 0 256 256" width="32" height="32">
                  <path d="M117.25,157.92a60,60,0,1,0-66.5,0A95.83,95.83,0,0,0,3.53,195.63a8,8,0,1,0,13.4,8.74,80,80,0,0,1,134.14,0,8,8,0,0,0,13.4-8.74A95.83,95.83,0,0,0,117.25,157.92ZM40,108a44,44,0,1,1,44,44A44.05,44.05,0,0,1,40,108Z"></path>
                </svg>
              </div>
              <h2 className="text-lg font-bold">Find a Freelancer</h2>
              <p className="text-sm text-gray-500">
                Browse our talent pool and select the best fit for your needs.
              </p>
            </div>
            {/* Card 3 */}
            <div className="flex flex-col gap-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm hover:shadow-lg transition">
              <div className="text-[#87CEEB]">
                <svg fill="currentColor" viewBox="0 0 256 256" width="32" height="32">
                  <path d="M128,24A104,104,0,1,0,232,128,104.11,104.11,0,0,0,128,24Zm0,192a88,88,0,1,1,88-88A88.1,88.1,0,0,1,128,216Zm48-88a8,8,0,0,1-8,8H136V80a8,8,0,0,1,16,0v40h24A8,8,0,0,1,176,128Z"></path>
                </svg>
              </div>
              <h2 className="text-lg font-bold">Collaborate</h2>
              <p className="text-sm text-gray-500">
                Work together seamlessly with our built-in tools and communication features.
              </p>
            </div>
          </div>
        </section>

        {/* Why Unhire Section */}
        <section className="px-4 py-20 bg-gray-50">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-extrabold">Why Choose Unhire?</h1>
            <p className="text-lg text-gray-600">
              We offer a streamlined experience for both clients and freelancers, ensuring successful project outcomes.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Card examples */}
            <div className="flex flex-col gap-4">
              <div
                className="w-full aspect-video bg-cover bg-center rounded-xl shadow-md"
                style={{
                  backgroundImage:
                    'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAZWRAoeLU2HRMyI2dLzqhFM4o-BA7knPEuOhAs9jWd-ae9JQ84SUvULRkGTiuBLwoOVovBTjwA2avqRIjigxiFp8fW8cRgkpo9ryeFO6m72BhFdYok_Uo0PkzFlb7P3jnBVKPgIU5_x-PUq11p84gdlWe6CLQGl3_fJLsmEdbpymUbhXexhdccoPLcfWq05kqztr7Q5Qygnuy6ZCAyoLfxddS8d33sSaaa1_mZKigpOU0Qjvt9oFZhIN-W7pMeI0tfK2TLk9AiJQd-")',
                }}
              ></div>
              <h3 className="text-lg font-bold">Instant Task Flow</h3>
              <p className="text-sm text-gray-500">
                Quickly find freelancers for immediate tasks with our instant job posting feature.
              </p>
            </div>
            <div className="flex flex-col gap-4">
              <div
                className="w-full aspect-video bg-cover bg-center rounded-xl shadow-md"
                style={{
                  backgroundImage:
                    'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDDDzkOqwgco3Lo-tFUQRker5eEwulpl_7LtjvGlJ2XWhDEMqWQaXuhlm_t-oRSuKdCJiGT4BsHvs2gPaFKaMN9rJILOvqscvBgQoaM0T0DT2HXlPVU6lU7PgXrS0PL-4z4IA7qj2nAETMsje7-o8IIXkqJQ5Y9BpTPhOsISPtY-YNugVXw0M0K93nLfLJ96I67bNB2LPSJdqfTCiQQvDIW6z13x_f-LeCN0D01DRxjdwlDeIDHkDZVJJasu7fyoZj_BPd9bj09bHep")',
                }}
              ></div>
              <h3 className="text-lg font-bold">Long-Term Collaboration</h3>
              <p className="text-sm text-gray-500">
                Build lasting partnerships with talented professionals for ongoing projects.
              </p>
            </div>
            <div className="flex flex-col gap-4">
              <div
                className="w-full aspect-video bg-cover bg-center rounded-xl shadow-md"
                style={{
                  backgroundImage:
                    'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCaJlMlfyy-odz6XKjZWwL7oqdSqqbBkd4KdutamiA51QPuvEjKqxnV-qIAhdNYDtN3ewO1WOwaUD2dXWamZm97N1u58_NzLtBcyR8_cUCjraNntykMXhUMq_VTW1RjMbUE6HHN6jor6bK1Nk2dv_Gyrf4nV5D0sC5ZilvAZ0uyOLoqKmSSy1oU4nIHAk_ZHROXfm2TNupMpr_50Msd_KrEBI6nesu36d8s6WHrK8IHUVTHxiY5RT19SjfZDYKbm96SmiRBYiS6zGz1")',
                }}
              ></div>
              <h3 className="text-lg font-bold">Secure Payments</h3>
              <p className="text-sm text-gray-500">
                Our secure payment system ensures timely and reliable transactions for all parties.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="flex justify-center border-t border-gray-200 bg-white">
        <div className="max-w-5xl flex-1 flex flex-col px-5 py-12 gap-8">
          <div className="flex flex-wrap justify-center gap-x-8 gap-y-4">
            <a href="#" className="text-sm text-gray-500 hover:text-gray-900">
              About
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-gray-900">
              Contact
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-gray-900">
              Terms of Service
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-gray-900">
              Privacy Policy
            </a>
          </div>
          <p className="text-sm text-gray-500 text-center">
            © 2024 Unhire. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
