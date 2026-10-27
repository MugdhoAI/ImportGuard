/// <reference types="vite/client" />

declare module "*?raw" {
  const source: string;
  export default source;
}

declare module "three128" {
  const three: any;
  export = three;
}

// The canonical ThreeUI dock source uses THREE.Mesh/Vector3 type names in
// addition to its namespace import. Keep the vendor files byte-identical.
declare namespace THREE {
  type Mesh = any;
  type ShaderMaterial = any;
  type Vector3 = any;
}
