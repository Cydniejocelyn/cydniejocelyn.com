import { useEffect } from 'react';

declare global {
  interface Window {
    FlodeskObject?: string;
    fd?: ((...args: any[]) => void) & { q?: IArguments[] };
    __fdLettersInit?: boolean;
  }
}

const FLODESK_FORM_ID = '6a8f553c9f30a024ac4f2a82';

export default function FlodeskPopup() {
  useEffect(() => {
    if (typeof window === 'undefined') return;

    if (!document.querySelector('script[src*="assets.flodesk.com"]')) {
      (function (w: any, d: Document, t: string, h: string, s: string, n: string) {
        w.FlodeskObject = n;
        const fn = function (this: any) {
          (w[n].q = w[n].q || []).push(arguments);
        };
        w[n] = w[n] || fn;

        const v = '?v=' + Math.floor(new Date().getTime() / (120 * 1000)) * 60;
        const target = d.head || d.getElementsByTagName('script')[0]?.parentNode;

        const sm = d.createElement(t) as HTMLScriptElement;
        sm.async = true;
        sm.type = 'module';
        sm.src = h + s + '.mjs' + v;
        target?.appendChild(sm);

        const sn = d.createElement(t) as HTMLScriptElement;
        sn.async = true;
        sn.noModule = true;
        sn.src = h + s + '.js' + v;
        target?.appendChild(sn);
      })(window, document, 'script', 'https://assets.flodesk.com', '/universal', 'fd');
    }

    if (window.__fdLettersInit) return;
    window.__fdLettersInit = true;

    window.fd?.('form', { formId: FLODESK_FORM_ID });
  }, []);

  return null;
}
