(function() {
      'use strict';

      // ---------- DOM refs ----------
      const products = document.querySelectorAll('.product-card');
      const grid = document.getElementById('grid');
      const emptyState = document.getElementById('emptyState');
      const resultCount = document.getElementById('resultCount');
      const activePills = document.getElementById('activePills');

      // Search
      const searchInput = document.getElementById('searchInput');
      const searchClear = document.getElementById('searchClear');

      // Category checkboxes
      const catChecks = document.querySelectorAll('.cat-check');
      const catReset = document.getElementById('catReset');

      // Nav links
      const navLinks = document.querySelectorAll('.nav-links a');

      // Dropdown
      const categoriesBtn = document.getElementById('categoriesBtn');
      const dropdownMenu = document.getElementById('dropdownMenu');

      // Mobile toggle
      const mobileToggle = document.getElementById('mobileToggle');
      const navList = document.getElementById('navLinks');

      // Favoritos y carrito (contadores)
      const favCount = document.getElementById('favCount');
      const cartCount = document.getElementById('cartCount');

      // Modal
      const modalOverlay = document.getElementById('modalOverlay');
      const modalClose = document.getElementById('modalClose');
      const modalMedia = document.getElementById('modalMedia');
      const modalCategory = document.getElementById('modalCategory');
      const modalTitle = document.getElementById('modalTitle');
      const modalRef = document.getElementById('modalRef');
      const modalDesc = document.getElementById('modalDesc');
      const modalPrice = document.getElementById('modalPrice');
      const modalAdd = document.getElementById('modalAdd');

      // Toast
      const toastContainer = document.getElementById('toastContainer');

      // ---------- Estado ----------
      let activeFilters = {
        search: '',
        categories: [], // array de 'capilar', 'facial', 'maquillaje'
        nav: 'inicio' // 'inicio' | 'capilar' | 'tiendas' | 'nueva'
      };

      let favorites = new Set(); // almacena referencias (data-ref)
      let cart = []; // almacena objetos { ref, title, price }

      // ---------- Funciones auxiliares ----------
      function getProductData(card) {
        return {
          category: card.dataset.category,
          new: card.dataset.new === 'true',
          store: card.dataset.store === 'true',
          title: card.dataset.title,
          ref: card.dataset.ref,
          price: parseInt(card.dataset.price, 10),
          desc: card.dataset.desc
        };
      }

      function formatPrice(p) {
        return '$ ' + p.toLocaleString('es-CO');
      }

      function showToast(msg) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = msg;
        toastContainer.appendChild(toast);
        setTimeout(() => {
          if (toast.parentNode) toast.remove();
        }, 2800);
      }

      // ---------- Renderizado / filtrado ----------
      function filterProducts() {
        const search = activeFilters.search.toLowerCase().trim();
        const cats = activeFilters.categories;
        const nav = activeFilters.nav;

        let visible = 0;

        products.forEach(card => {
          const data = getProductData(card);
          const title = data.title.toLowerCase();
          const ref = data.ref.toLowerCase();
          const desc = (data.desc || '').toLowerCase();

          // Buscador
          let matchSearch = true;
          if (search) {
            matchSearch = title.includes(search) || ref.includes(search) || desc.includes(search);
          }

          // Categorías (si hay alguna seleccionada)
          let matchCat = true;
          if (cats.length > 0) {
            matchCat = cats.includes(data.category);
          }

          // Nav
          let matchNav = true;
          if (nav === 'capilar') {
            matchNav = data.category === 'capilar';
          } else if (nav === 'tiendas') {
            matchNav = data.store === true;
          } else if (nav === 'nueva') {
            matchNav = data.new === true;
          } // 'inicio' -> todos

          const show = matchSearch && matchCat && matchNav;
          card.style.display = show ? '' : 'none';
          if (show) visible++;
        });

        // Actualizar contador
        resultCount.textContent = visible;
        emptyState.hidden = visible > 0;

        // Actualizar pills
        renderPills();

        // Marcar enlace activo
        navLinks.forEach(link => {
          const navVal = link.dataset.nav;
          link.classList.toggle('active-link', navVal === nav);
        });
      }

      // ---------- Pills (filtros activos) ----------
      function renderPills() {
        const pills = [];
        const search = activeFilters.search.trim();
        if (search) {
          pills.push({ label: `"${search}"`, type: 'search' });
        }
        activeFilters.categories.forEach(cat => {
          pills.push({ label: cat.charAt(0).toUpperCase() + cat.slice(1), type: 'category', value: cat });
        });
        const nav = activeFilters.nav;
        if (nav === 'capilar') pills.push({ label: 'Capilar', type: 'nav' });
        else if (nav === 'tiendas') pills.push({ label: 'Tiendas', type: 'nav' });
        else if (nav === 'nueva') pills.push({ label: 'Nueva Colección', type: 'nav' });

        if (pills.length === 0) {
          activePills.innerHTML = '';
          return;
        }

        let html = '';
        pills.forEach((p, idx) => {
          html += `<span class="pill">
            ${p.label}
            <span class="remove-pill" data-idx="${idx}" data-type="${p.type}" data-value="${p.value || ''}">✕</span>
          </span>`;
        });
        activePills.innerHTML = html;

        // Event listeners para eliminar pills
        activePills.querySelectorAll('.remove-pill').forEach(el => {
          el.addEventListener('click', function() {
            const type = this.dataset.type;
            const value = this.dataset.value;
            if (type === 'search') {
              searchInput.value = '';
              activeFilters.search = '';
              searchClear.hidden = true;
            } else if (type === 'category') {
              const check = document.querySelector(`.cat-check[value="${value}"]`);
              if (check) check.checked = false;
              const idx = activeFilters.categories.indexOf(value);
              if (idx > -1) activeFilters.categories.splice(idx, 1);
            } else if (type === 'nav') {
              // resetear nav a 'inicio'
              activeFilters.nav = 'inicio';
            }
            filterProducts();
          });
        });
      }

      // ---------- Eventos de búsqueda ----------
      searchInput.addEventListener('input', function() {
        const val = this.value;
        activeFilters.search = val;
        searchClear.hidden = !val;
        filterProducts();
      });

      searchClear.addEventListener('click', function() {
        searchInput.value = '';
        activeFilters.search = '';
        this.hidden = true;
        filterProducts();
        searchInput.focus();
      });

      // ---------- Eventos de categorías (checkboxes) ----------
      catChecks.forEach(check => {
        check.addEventListener('change', function() {
          const val = this.value;
          if (this.checked) {
            if (!activeFilters.categories.includes(val)) {
              activeFilters.categories.push(val);
            }
          } else {
            const idx = activeFilters.categories.indexOf(val);
            if (idx > -1) activeFilters.categories.splice(idx, 1);
          }
          filterProducts();
        });
      });

      catReset.addEventListener('click', function() {
        catChecks.forEach(c => c.checked = false);
        activeFilters.categories = [];
        filterProducts();
      });

      // ---------- Eventos de navegación (nav) ----------
      navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          const navVal = this.dataset.nav;
          // Si es 'inicio' o 'tiendas' o 'nueva' o 'capilar'
          if (navVal === 'inicio') {
            activeFilters.nav = 'inicio';
          } else if (navVal === 'capilar') {
            activeFilters.nav = 'capilar';
          } else if (navVal === 'tiendas') {
            activeFilters.nav = 'tiendas';
          } else if (navVal === 'nueva') {
            activeFilters.nav = 'nueva';
          } else {
            activeFilters.nav = 'inicio';
          }
          // Cerrar menú móvil si está abierto
          if (navList.classList.contains('open')) {
            navList.classList.remove('open');
            mobileToggle.setAttribute('aria-expanded', 'false');
          }
          filterProducts();
          // Scroll al grid (opcional)
          document.getElementById('grid').scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      });

      // ---------- Dropdown categorías ----------
      categoriesBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        const expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', !expanded);
        dropdownMenu.classList.toggle('show');
      });

      document.addEventListener('click', function(e) {
        if (!e.target.closest('.categories-container')) {
          dropdownMenu.classList.remove('show');
          categoriesBtn.setAttribute('aria-expanded', 'false');
        }
      });

      // ---------- Mobile toggle ----------
      mobileToggle.addEventListener('click', function() {
        const expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', !expanded);
        navList.classList.toggle('open');
      });

      // ---------- Favoritos ----------
      document.querySelectorAll('.btn-fav').forEach(btn => {
        btn.addEventListener('click', function(e) {
          e.stopPropagation();
          const card = this.closest('.product-card');
          if (!card) return;
          const ref = card.dataset.ref;
          if (!ref) return;
          const isFav = favorites.has(ref);
          if (isFav) {
            favorites.delete(ref);
            this.classList.remove('active');
            this.setAttribute('aria-pressed', 'false');
            showToast('Eliminado de favoritos');
          } else {
            favorites.add(ref);
            this.classList.add('active');
            this.setAttribute('aria-pressed', 'true');
            showToast('Agregado a favoritos ❤️');
          }
          favCount.textContent = favorites.size;
          favCount.hidden = favorites.size === 0;
        });
      });

      // ---------- Carrito ----------
      document.querySelectorAll('.btn-add').forEach(btn => {
        btn.addEventListener('click', function(e) {
          e.stopPropagation();
          const card = this.closest('.product-card');
          if (!card) return;
          const ref = card.dataset.ref;
          const title = card.dataset.title;
          const price = parseInt(card.dataset.price, 10);
          if (!ref || !title) return;
          // Verificar si ya está en el carrito
          const existing = cart.find(item => item.ref === ref);
          if (existing) {
            showToast('Ya está en el carrito');
            return;
          }
          cart.push({ ref, title, price });
          cartCount.textContent = cart.length;
          cartCount.hidden = cart.length === 0;
          showToast(`"${title}" agregado al carrito 🛒`);
        });
      });

      // ---------- Vista rápida (modal) ----------
      document.querySelectorAll('.btn-view').forEach(btn => {
        btn.addEventListener('click', function(e) {
          e.stopPropagation();
          const card = this.closest('.product-card');
          if (!card) return;
          const data = getProductData(card);
          const imgSrc = card.querySelector('.product-media img')?.src || '';
          const marca = card.querySelector('.product-ref')?.textContent || '';
          // Llenar modal
          modalMedia.innerHTML = `<img src="${imgSrc}" alt="${data.title}" loading="lazy">`;
          modalCategory.textContent = data.category.charAt(0).toUpperCase() + data.category.slice(1);
          modalTitle.textContent = data.title;
          modalRef.textContent = marca;
          modalDesc.textContent = data.desc || 'Sin descripción';
          modalPrice.textContent = formatPrice(data.price);
          modalAdd.dataset.ref = data.ref;
          modalAdd.dataset.title = data.title;
          modalAdd.dataset.price = data.price;
          modalOverlay.hidden = false;
        });
      });

      modalClose.addEventListener('click', function() {
        modalOverlay.hidden = true;
      });

      modalOverlay.addEventListener('click', function(e) {
        if (e.target === this) modalOverlay.hidden = true;
      });

      // Botón agregar del modal
      modalAdd.addEventListener('click', function() {
        const ref = this.dataset.ref;
        const title = this.dataset.title;
        const price = parseInt(this.dataset.price, 10);
        if (!ref || !title) return;
        const existing = cart.find(item => item.ref === ref);
        if (existing) {
          showToast('Ya está en el carrito');
          return;
        }
        cart.push({ ref, title, price });
        cartCount.textContent = cart.length;
        cartCount.hidden = cart.length === 0;
        showToast(`"${title}" agregado al carrito 🛒`);
        modalOverlay.hidden = true;
      });

      // ---------- Hero carrusel ----------
      const heroTrack = document.getElementById('heroTrack');
      const heroDots = document.getElementById('heroDots');
      const slides = heroTrack.querySelectorAll('.hero-slide');
      let currentSlide = 0;
      let totalSlides = slides.length;

      // Crear dots
      slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.setAttribute('role', 'tab');
        dot.setAttribute('aria-label', `Diapositiva ${i+1}`);
        if (i === 0) dot.classList.add('active-dot');
        dot.addEventListener('click', () => goToSlide(i));
        heroDots.appendChild(dot);
      });

      function goToSlide(index) {
        if (index < 0) index = totalSlides - 1;
        if (index >= totalSlides) index = 0;
        currentSlide = index;
        heroTrack.style.transform = `translateX(-${currentSlide * 100}%)`;
        document.querySelectorAll('.hero-dots button').forEach((d, i) => {
          d.classList.toggle('active-dot', i === currentSlide);
        });
      }

      document.getElementById('heroPrev').addEventListener('click', () => goToSlide(currentSlide - 1));
      document.getElementById('heroNext').addEventListener('click', () => goToSlide(currentSlide + 1));

      // Auto-play (opcional)
      let heroInterval = setInterval(() => goToSlide(currentSlide + 1), 5000);
      document.querySelector('.hero').addEventListener('mouseenter', () => clearInterval(heroInterval));
      document.querySelector('.hero').addEventListener('mouseleave', () => {
        heroInterval = setInterval(() => goToSlide(currentSlide + 1), 5000);
      });

      // ---------- Inicializar ----------
      filterProducts();

      // Contadores iniciales
      cartCount.hidden = true;
      favCount.hidden = true;

    })();