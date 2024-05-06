// // See https://kit.svelte.dev/docs/types#app
// // for information about these interfaces
// declare global {
// 	namespace App {
// 		// interface Error {}
// 		// interface Locals {}
// 		// interface PageData {}
// 		// interface Platform {}
// 	}
// }
//
// export {};
//

declare global {
    namespace App {
        interface Locals {
            auth: Auth
        }
        interface PageData {
            session: Session | null
        }
        // interface Error {}
        // interface Platform {}
        // 
    }
}

export { };
